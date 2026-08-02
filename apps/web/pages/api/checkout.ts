import { buffer } from "micro";
import type { NextApiRequest, NextApiResponse } from "next";
import Stripe from "stripe";

import { auth } from "@/lib/auth";
import { db } from "@/lib/db";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY ?? "", {
  apiVersion: "2024-04-10",
});

const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET ?? "";

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") {
    res.setHeader("Allow", ["POST"]);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }

  if (req.headers["stripe-signature"]) {
    const payload = await buffer(req);
    const signature = req.headers["stripe-signature"];

    let event: Stripe.Event;
    try {
      event = stripe.webhooks.constructEvent(payload.toString(), signature, endpointSecret);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown error";
      return res.status(400).send(`Webhook Error: ${message}`);
    }

    if (event.type === "checkout.session.completed") {
      await handleCheckoutSessionCompleted(event);
    } else if (event.type === "invoice.payment_succeeded") {
      await handleInvoicePaymentSucceeded(event);
    }

    return res.status(200).json({ received: true });
  }

  return handleCheckoutCreation(req, res);
}

async function handleCheckoutSessionCompleted(event: Stripe.Event) {
  const checkoutSession = event.data.object as Stripe.Checkout.Session;

  if (!checkoutSession.subscription || !checkoutSession.customer_email) {
    return;
  }

  const user = await db.user.findUnique({
    where: { email: checkoutSession.customer_email },
  });

  if (!user) {
    return;
  }

  const subscription = await stripe.subscriptions.retrieve(checkoutSession.subscription as string);

  await db.user.update({
    where: { id: user.id },
    data: {
      stripeSubscriptionId: subscription.id,
      stripePriceId: subscription.items.data[0]?.price.id,
      stripeCurrentPeriodEnd: new Date(subscription.current_period_end * 1000),
      hasPaid: true,
    },
  });
}

async function handleInvoicePaymentSucceeded(event: Stripe.Event) {
  const invoice = event.data.object as Stripe.Invoice;
  const subscriptionId = invoice.subscription as string | null;

  if (!subscriptionId || !invoice.customer_email) {
    return;
  }

  const subscription = await stripe.subscriptions.retrieve(subscriptionId);
  const user = await db.user.findUnique({
    where: { email: invoice.customer_email },
  });

  if (!user) {
    return;
  }

  await db.user.update({
    where: { id: user.id },
    data: {
      stripeCurrentPeriodEnd: new Date(subscription.current_period_end * 1000),
    },
  });
}

async function handleCheckoutCreation(req: NextApiRequest, res: NextApiResponse) {
  const session = await auth(req, res);

  if (!session?.user?.id) {
    return res.status(401).json({ error: "Unauthorized" });
  }

  const origin = req.headers.origin ?? process.env.NEXT_PUBLIC_APP_URL;
  if (!origin) {
    return res.status(500).json({ error: "Application URL is not configured" });
  }

  const checkoutSession = await stripe.checkout.sessions.create({
    payment_method_types: ["card"],
    line_items: [
      {
        price: "price_1PS6GtAPpzV89AesFYQwxtij",
        quantity: 1,
      },
    ],
    mode: "subscription",
    customer_email: session.user.email ?? undefined,
    success_url: `${origin}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${origin}/pricing`,
  });

  return res.status(200).json({ url: checkoutSession.url });
}

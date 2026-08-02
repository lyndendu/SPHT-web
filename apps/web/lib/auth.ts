import { PrismaAdapter } from "@auth/prisma-adapter";
import { nanoid } from "nanoid";
import NextAuth from "next-auth";
import Google from "next-auth/providers/google";

import { db } from "@/lib/db";

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(db),
  session: {
    strategy: "jwt",
  },
  pages: {
    signIn: "/login",
  },
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),
  ],
  callbacks: {
    async session({ token, session }) {
      if (session.user) {
        const userId = token.id ?? token.sub;
        if (userId) {
          session.user.id = userId;
        }
        session.user.name = token.name ?? session.user.name;
        session.user.email = token.email ?? session.user.email;
        session.user.image = token.picture ?? session.user.image;
        session.user.username = token.username ?? null;
      }

      return session;
    },
    async jwt({ token, user }) {
      if (!token.email) {
        if (user?.id) {
          token.id = user.id;
        }
        return token;
      }

      const dbUser = await db.user.findFirst({
        where: {
          email: token.email,
        },
      });

      if (!dbUser) {
        if (user?.id) {
          token.id = user.id;
        }
        return token;
      }

      let username = dbUser.username;
      if (!username) {
        const updatedUser = await db.user.update({
          where: {
            id: dbUser.id,
          },
          data: {
            username: nanoid(10),
          },
        });
        username = updatedUser.username;
      }

      return {
        ...token,
        id: dbUser.id,
        name: dbUser.name,
        email: dbUser.email,
        picture: dbUser.image,
        username,
      };
    },
    authorized({ auth: session, request }) {
      const isAuthenticated = Boolean(session?.user);
      const pathname = request.nextUrl.pathname;
      const isAuthPage = pathname.startsWith("/login") || pathname.startsWith("/register");
      const isProtectedPage = pathname.startsWith("/dashboard") || pathname.startsWith("/editor");

      if (isAuthPage && isAuthenticated) {
        return Response.redirect(new URL("/dashboard", request.nextUrl));
      }

      if (isProtectedPage) {
        return isAuthenticated;
      }

      return true;
    },
  },
});

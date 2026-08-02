from __future__ import annotations

import json
from pathlib import Path

package_path = Path("package.json")
package = json.loads(package_path.read_text(encoding="utf-8"))
package["pnpm"] = {
    "onlyBuiltDependencies": [
        "@prisma/client",
        "@prisma/engines",
        "@vercel/speed-insights",
        "prisma",
        "sharp",
    ]
}
package_path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")

print("Trusted pnpm dependency build scripts configured.")

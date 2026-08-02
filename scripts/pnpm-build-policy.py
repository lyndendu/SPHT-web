from __future__ import annotations

import json
from pathlib import Path

package_path = Path("package.json")
package = json.loads(package_path.read_text(encoding="utf-8"))
package.pop("pnpm", None)
package_path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")

workspace_path = Path("pnpm-workspace.yaml")
workspace_path.write_text(
    "packages:\n"
    "  - 'apps/*'\n"
    "  - 'packages/*'\n"
    "\n"
    "onlyBuiltDependencies:\n"
    "  - '@prisma/client'\n"
    "  - '@prisma/engines'\n"
    "  - '@vercel/speed-insights'\n"
    "  - 'prisma'\n"
    "  - 'sharp'\n",
    encoding="utf-8",
)

print("Trusted pnpm dependency build scripts configured in workspace settings.")

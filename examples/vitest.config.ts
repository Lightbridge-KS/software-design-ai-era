import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    include: ["ch*/ts/**/*.test.ts"],
    environment: "node",
  },
});

FROM node:24-bookworm-slim AS builder
WORKDIR /application
ENV NEXT_TELEMETRY_DISABLED=1
COPY package*.json ./
RUN npm ci
COPY app ./app
COPY components ./components
COPY lib ./lib
COPY tsconfig.json next-env.d.ts ./
RUN npm run build

FROM node:24-bookworm-slim AS runtime
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1
WORKDIR /application
COPY --from=builder --chown=node:node /application ./
USER node
EXPOSE 3000
CMD ["node", "node_modules/next/dist/bin/next", "start", "--hostname", "0.0.0.0", "--port", "3000"]

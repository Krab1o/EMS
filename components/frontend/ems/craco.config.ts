// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
module.exports = {
  webpack: {
    configure: {
      ignoreWarnings: [/Failed to parse source map.*react-keycloak/],
    },
  },
};

export const api = window.axios.create({
  baseURL: window.location.origin,
  timeout: 10000,
  headers: {
    Accept: "application/json",
  },
});

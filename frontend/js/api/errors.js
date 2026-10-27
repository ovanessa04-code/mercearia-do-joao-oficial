export function normalizarErro(error) {
  if (window.axios.isCancel(error)) {
    return null;
  }

  if (error.code === "ECONNABORTED" || error.code === "ETIMEDOUT") {
    return "A API demorou para responder. Tente novamente.";
  }

  if (!error.response) {
    return "Não foi possível acessar a API.";
  }

  const { status, data } = error.response;

  if (Array.isArray(data?.detail)) {
    return data.detail.map((item) => item.msg).join(" ");
  }

  if (typeof data?.detail === "string") {
    return data.detail;
  }

  const mensagens = {
    401: "Sua sessão não está autorizada.",
    403: "Você não possui permissão para esta ação.",
    404: "Cliente não encontrado.",
    409: "A operação entrou em conflito com os dados atuais.",
  };

  if (mensagens[status]) {
    return mensagens[status];
  }

  if (status >= 500) {
    return "A API está indisponível no momento.";
  }

  return "Não foi possível concluir a operação.";
}

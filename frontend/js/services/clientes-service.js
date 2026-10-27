import { api } from "../api/client.js";


export async function listarClientes(signal) {
  const response = await api.get("/clientes", { signal });
  return response.data;
}

export async function cadastrarCliente(dados) {
  const response = await api.post("/clientes", dados);
  return response.data;
}

export async function atualizarCliente(idCliente, dados) {
  const response = await api.put(`/clientes/${idCliente}`, dados);
  return response.data;
}

export async function excluirCliente(idCliente) {
  await api.delete(`/clientes/${idCliente}`);
}

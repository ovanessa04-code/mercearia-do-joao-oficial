import { normalizarErro } from "./api/errors.js";
import {
  atualizarCliente,
  cadastrarCliente,
  excluirCliente,
  listarClientes,
} from "./services/clientes-service.js";


const formulario = document.querySelector("#cliente-form");
const tituloFormulario = document.querySelector("#titulo-formulario");
const nomeInput = document.querySelector("#nome_cliente");
const nascimentoInput = document.querySelector("#data_nascimento");
const limiteInput = document.querySelector("#valor_limite");
const salvarButton = document.querySelector("#salvar");
const cancelarButton = document.querySelector("#cancelar-edicao");
const recarregarButton = document.querySelector("#recarregar");
const lista = document.querySelector("#clientes-lista");
const mensagem = document.querySelector("#mensagem");

let idEmEdicao = null;
let carregamentoAtual = null;
let sequenciaCarregamento = 0;

const formatadorMoeda = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});


function exibirMensagem(texto = "", tipo = "") {
  mensagem.textContent = texto;
  mensagem.dataset.type = tipo;
}


function definirFormularioOcupado(ocupado) {
  formulario.querySelectorAll("input, button").forEach((elemento) => {
    elemento.disabled = ocupado;
  });
  salvarButton.textContent = ocupado ? "Salvando..." : "Salvar";
}


function encerrarEdicao() {
  idEmEdicao = null;
  formulario.reset();
  tituloFormulario.textContent = "Novo cliente";
  cancelarButton.hidden = true;
}


function iniciarEdicao(cliente) {
  idEmEdicao = cliente.id_cliente;
  nomeInput.value = cliente.nome_cliente;
  nascimentoInput.value = cliente.data_nascimento;
  limiteInput.value = cliente.valor_limite;
  tituloFormulario.textContent = `Editar cliente #${cliente.id_cliente}`;
  cancelarButton.hidden = false;
  nomeInput.focus();
  formulario.scrollIntoView({ behavior: "smooth", block: "center" });
}


function criarBotao(texto, classe, aoClicar) {
  const botao = document.createElement("button");
  botao.type = "button";
  botao.className = `button button-small ${classe}`;
  botao.textContent = texto;
  botao.addEventListener("click", aoClicar);
  return botao;
}


function criarCelula(texto) {
  const celula = document.createElement("td");
  celula.textContent = texto;
  return celula;
}


function renderizarClientes(clientes) {
  lista.replaceChildren();

  if (!clientes.length) {
    const linha = document.createElement("tr");
    const celula = document.createElement("td");
    celula.colSpan = 4;
    celula.className = "empty-state";
    celula.textContent = "Nenhum cliente cadastrado.";
    linha.append(celula);
    lista.append(linha);
    return;
  }

  clientes.forEach((cliente) => {
    const linha = document.createElement("tr");
    const acoes = document.createElement("td");
    const grupoAcoes = document.createElement("div");
    grupoAcoes.className = "row-actions";

    const editarButton = criarBotao(
      "Editar",
      "button-secondary",
      () => iniciarEdicao(cliente),
    );
    const excluirButton = criarBotao(
      "Excluir",
      "button-danger",
      () => removerCliente(cliente, excluirButton),
    );

    grupoAcoes.append(editarButton, excluirButton);
    acoes.append(grupoAcoes);
    linha.append(
      criarCelula(cliente.nome_cliente),
      criarCelula(cliente.data_nascimento),
      criarCelula(formatadorMoeda.format(Number(cliente.valor_limite))),
      acoes,
    );
    lista.append(linha);
  });
}


async function carregarClientes() {
  carregamentoAtual?.abort();
  carregamentoAtual = new AbortController();
  const sequencia = ++sequenciaCarregamento;

  recarregarButton.disabled = true;
  lista.setAttribute("aria-busy", "true");
  exibirMensagem("Carregando clientes...");

  try {
    const clientes = await listarClientes(carregamentoAtual.signal);
    if (sequencia !== sequenciaCarregamento) return;
    renderizarClientes(clientes);
    exibirMensagem();
  } catch (error) {
    const texto = normalizarErro(error);
    if (texto && sequencia === sequenciaCarregamento) {
      renderizarClientes([]);
      exibirMensagem(texto, "error");
    }
  } finally {
    if (sequencia === sequenciaCarregamento) {
      recarregarButton.disabled = false;
      lista.removeAttribute("aria-busy");
    }
  }
}


async function removerCliente(cliente, botao) {
  const confirmou = window.confirm(`Excluir ${cliente.nome_cliente}?`);
  if (!confirmou) return;

  botao.disabled = true;
  exibirMensagem("Excluindo cliente...");

  try {
    await excluirCliente(cliente.id_cliente);
    if (idEmEdicao === cliente.id_cliente) encerrarEdicao();
    await carregarClientes();
    exibirMensagem("Cliente excluído.", "success");
  } catch (error) {
    exibirMensagem(normalizarErro(error), "error");
    botao.disabled = false;
  }
}


formulario.addEventListener("submit", async (event) => {
  event.preventDefault();
  definirFormularioOcupado(true);
  exibirMensagem(idEmEdicao ? "Atualizando cliente..." : "Salvando cliente...");

  const dados = {
    nome_cliente: nomeInput.value,
    data_nascimento: nascimentoInput.value,
    valor_limite: limiteInput.value,
  };

  try {
    if (idEmEdicao) {
      await atualizarCliente(idEmEdicao, dados);
    } else {
      await cadastrarCliente(dados);
    }

    const mensagemSucesso = idEmEdicao
      ? "Cliente atualizado."
      : "Cliente cadastrado.";
    encerrarEdicao();
    await carregarClientes();
    exibirMensagem(mensagemSucesso, "success");
  } catch (error) {
    exibirMensagem(normalizarErro(error), "error");
  } finally {
    definirFormularioOcupado(false);
  }
});

cancelarButton.addEventListener("click", encerrarEdicao);
recarregarButton.addEventListener("click", carregarClientes);
window.addEventListener("beforeunload", () => carregamentoAtual?.abort());

carregarClientes();

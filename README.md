# 📦 transforms\_fake

> Gera imagens sintéticas realistas para treinar modelos de segmentação de forma inteligente, simples e divertida.

![badge](https://img.shields.io/badge/version-0.1.0-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

---

## ✨ O que é?

`transforms_fake` é uma biblioteca Python que cria **novas imagens e máscaras** automaticamente a partir de outras já rotuladas (com máscaras). Ideal para **segmentação de imagens**, especialmente quando você não tem muitos dados rotulados.

Ao contrário de bibliotecas como `Albumentations`, que apenas transformam o que já existe (flip, blur, crop etc), esta aqui cria **novos exemplos** inserindo objetos reais com contexto em outras imagens de forma automática.

Imagine pegar um tomate de uma imagem, girar um pouco e colar ele em outro canto da mesma ou de outra imagem. Isso, com máscaras e sem sofrimento. É isso que a `transforms_fake` faz. 🍅📸✨

---

## 🎯 Motivacão

Quantas vezes você já quis treinar um modelo, mas não tinha dados suficientes? E se fosse possível multiplicar seus dados sem perder realismo?

`transforms_fake` nasce dessa necessidade: **aumentar conjuntos de dados de forma contextual e realista, focando em segmentação**.

---

## 📌 Exemplos Visuais

### Original:

![original](https://via.placeholder.com/300x200?text=Imagem+Original)

### Após `transforms_fake`:

![gerado](https://via.placeholder.com/300x200?text=Imagem+Gerada)

> Veja como objetos foram reposicionados de forma realista, mantendo a coerência com máscaras!

---

## 🧠 Como funciona?

1. **Lê imagens e máscaras** (por exemplo, PNG com canal alpha ou imagens separadas)
2. Detecta instâncias rotuladas
3. Faz "recorte" do objeto com base na máscara
4. Reinsere em outra região da imagem (com opções de rotação, flip, escala etc)
5. Atualiza a máscara automaticamente

---

## ✅ Recursos

| Recurso                                 | Suporte |
| --------------------------------------- | ------- |
| Copy-paste com máscaras                 | ✅       |
| Rotação, flip, escala contextual        | ✅       |
| Inserção em outra imagem                | ✅       |
| Suporte a PyTorch e FastAI              | ✅       |
| Atualização de máscaras automática      | ✅       |
| Exporta como dataset (imagens + labels) | ✅       |

---

## 🚀 Instalação

```bash
pip install transforms_fake
```

Ou diretamente do GitHub (versão mais recente):

```bash
pip install git+https://github.com/THOTIACORP/transforms_fake.git
```

---

## 🧪 Exemplo de uso

```python
from transforms_fake import main

main(
    input_dir="./meu_dataset",
    output_dir="./dataset_aumentado",
    num_augmented=50,
    rotate=True,
    flip=True,
    paste_in_different_images=True
)
```

---

## 🧱 Estrutura sugerida

```
meu_dataset/
├── images/
│   ├── img1.png
│   └── img2.png
└── masks/
    ├── img1_mask.png
    └── img2_mask.png
```

---

## 🤖 Comparativo com Albumentations

| Recurso                            | Albumentations | transforms\_fake |
| ---------------------------------- | -------------- | ---------------- |
| Transformar imagem original        | ✅              | ✅                |
| Gera novas instâncias realistas    | ❌              | ✅                |
| Manipula objetos individuais       | ❌              | ✅                |
| Reutiliza máscaras para colagem    | ❌              | ✅                |
| Modo interativo (com GUI opcional) | ❌              | ✅ (em breve)     |

---

🔬 Comparativo com a Sinapsis

| 🔧 Recurso                              | Sinapsis Tools (Albumentations Wrappers) | transforms\_fake                |
| --------------------------------------- | ---------------------------------------- | ------------------------------- |
| Rotação, flip, elastic, warp            | ✅                                        | ✅                               |
| Suporte a máscaras & keypoints          | ✅                                        | ✅                               |
| Copy-paste por objeto (instância)       | ❌                                        | ✅                               |
| Geração de imagens sintéticas realistas | ❌                                        | ✅                               |
| Interface gráfica / demo (web ou GUI)   | ✅ (Gradio/webapp)                        | ✅ (GUI Qt - em desenvolvimento) |


---

## 👵 Para a Tia Maria entender

Imagina que você tem uma foto de uma banana. Agora, você quer treinar um computador pra reconhecer bananas, mas só tem 3 fotos. Com essa biblioteca, você pode:

* Copiar a banana da primeira imagem,
* Girar um pouco,
* Colar em outro canto,
* E repetir!

Agora o computador acha que você tem 50 fotos diferentes. 🍌🧠

---

## 📚 Documentação (em breve)

Enquanto isso, veja os exemplos em `examples/` ou explore os notebooks.

---

## 🛠 Requisitos

* Python 3.8+
* OpenCV
* NumPy
* Pillow
* matplotlib (opcional)
* PyQt5 (futuro suporte a modo visual)

---

## 👨‍💻 Contribuindo

Pull requests são bem-vindos! Para bugs, abra uma issue. Para sugestões, nos mande um email ou crie uma discussão.

---

## ✉️ Contato

THOTIACORP - [GitHub](https://github.com/THOTIACORP) | email: [founder@thotiacorp.com.br](mailto:founder@thotiacorp.com.br)

---

## 👉 Licença

GNU GENERAL PUBLIC LICENSE - use, copie, melhore!

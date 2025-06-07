# Transforms Fake

Uma biblioteca Python para gerar variações de imagens com objetos rotacionados e posicionamento aleatório, ideal para aumento de dados (data augmentation) em projetos de visão computacional.

## 🚀 Características

- **Rotação inteligente**: Aplica rotações aleatórias em objetos segmentados por máscaras
- **Posicionamento aleatório**: Coloca objetos em posições aleatórias sobre fundos limpos
- **Fundos limpos**: Gera automaticamente fundos sem os objetos originais
- **Interface gráfica**: GUI intuitiva para facilitar o uso
- **API programática**: Use diretamente em seus scripts Python
- **Máscaras preservadas**: Mantém as máscaras de segmentação correspondentes

## 📦 Instalação

### Instalação Básica (apenas funcionalidades essenciais)

```bash
pip install transforms-fake
```

### Instalação Completa (todas as dependências do seu ambiente)

```bash
pip install transforms-fake[full]
```

### Instalação para Desenvolvimento

```bash
pip install transforms-fake[dev]
```

### Instalação para API Web

```bash
pip install transforms-fake[api]
```

### Instalação para Visualização

```bash
pip install transforms-fake[viz]
```

### Instalação Manual (para desenvolvimento)

```bash
git clone https://github.com/seuusuario/transforms-fake.git
cd transforms-fake
pip install -e .              # Instalação básica
pip install -e .[full]        # Instalação completa
```

### Dependências

**Dependências Mínimas:**

- opencv-contrib-python (processamento de imagem)
- numpy (operações matemáticas)
- PyQt5 (interface gráfica)

**Dependências Completas (seu ambiente):**

- opencv-contrib-python, opencv-python
- numpy, pillow, matplotlib, plotly
- tqdm (barras de progresso)
- json5 (manipulação JSON)
- torchvision, scikit-learn (ML/DL)
- PyQt5, PyQt5-tools (interface)
- fastapi, uvicorn (API web)

## 🎯 Como usar

### Interface Gráfica

Execute a interface gráfica:

```bash
transforms-fake-gui
```

Ou via Python:

```python
from transforms_fake.gui import main
main()
```

### API Programática

```python
from transforms_fake import ImageTransformer

# Criar o transformador
transformer = ImageTransformer(target_size=(1428, 1068))

# Processar imagens
stats = transformer.process_images(
    image_dir='path/to/images',
    mask_dir='path/to/masks',
    output_dir='path/to/output',
    num_backgrounds=5,
    num_variations_per_background=10,
    rotation_range=(-180, 180),
    mask_classes=[1, 2, 3]
)

print(f"Processadas {stats['images_processed']} imagens")
print(f"Criadas {stats['total_variations_created']} variações")
```

### Exemplo Completo

```python
import os
from transforms_fake import ImageTransformer

def exemplo_completo():
    # Configurar caminhos
    image_dir = "dados/imagens"
    mask_dir = "dados/mascaras"
    output_dir = "dados/saida"

    # Criar transformador
    transformer = ImageTransformer(target_size=(1024, 768))

    # Função de callback para logging
    def log_callback(message):
        print(f"[LOG] {message}")

    # Processar imagens
    resultados = transformer.process_images(
        image_dir=image_dir,
        mask_dir=mask_dir,
        output_dir=output_dir,
        num_backgrounds=3,
        num_variations_per_background=5,
        rotation_range=(-45, 45),  # Rotação limitada
        mask_classes=[1, 2, 3],    # Classes que representam o objeto
        log_callback=log_callback
    )

    return resultados

if __name__ == "__main__":
    stats = exemplo_completo()
    print("Processamento concluído!")
    print(f"Estatísticas: {stats}")
```

## 📁 Estrutura de Diretórios

### Entrada esperada:

```
projeto/
├── imagens/
│   ├── img001.jpg
│   ├── img002.jpg
│   └── ...
└── mascaras/
    ├── img001.png
    ├── img002.png
    └── ...
```

### Saída gerada:

```
saida/
├── fundos_sem_objeto/
│   ├── fundo_limpo_img001.jpg
│   └── ...
├── variações/
│   ├── img001_var1.png
│   ├── img001_var2.png
│   └── ...
└── máscaras/
    ├── img001_var1_mask.png
    ├── img001_var2_mask.png
    └── ...
```

## ⚙️ Parâmetros

### ImageTransformer

- `target_size`: Tupla (largura, altura) para redimensionar imagens (padrão: (1428, 1068))

### process_images()

- `image_dir`: Diretório contendo as imagens originais
- `mask_dir`: Diretório contendo as máscaras correspondentes
- `output_dir`: Diretório base para salvar os resultados
- `num_backgrounds`: Número de imagens a usar como base (padrão: 5)
- `num_variations_per_background`: Número de variações por imagem (padrão: 10)
- `rotation_range`: Tupla (min, max) para ângulos de rotação em graus (padrão: (-180, 180))
- `mask_classes`: Lista de valores de classe na máscara que representam o objeto (padrão: [1, 2, 3])
- `log_callback`: Função opcional para logging

## 🔧 Funções Utilitárias

```python
from transforms_fake.utils import rotate_image_and_mask, find_background_patch

# Rotacionar imagem e máscara
img_rotated, mask_rotated = rotate_image_and_mask(image, mask, angle=45)

# Encontrar região de fundo
patch_pos = find_background_patch(mask, width=100, height=100, exclude_rect=(x, y, w, h))
```

## 📊 Formato das Máscaras

As máscaras devem ser imagens em escala de cinza onde:

- `0`: Representa o fundo
- `1, 2, 3, ...`: Representam diferentes classes do objeto (configurável via `mask_classes`)

## 🐛 Solução de Problemas

### Erro: "Nenhuma máscara encontrada"

- Verifique se os nomes dos arquivos de máscara correspondem aos das imagens
- As máscaras devem ter o mesmo nome base das imagens (exemplo: `img001.jpg` → `img001.png`)

### Erro: "Nenhum objeto encontrado na máscara"

- Verifique se as máscaras contêm os valores de classe corretos
- Ajuste o parâmetro `mask_classes` conforme necessário

### Erro: "Não foi possível criar fundo limpo"

- A imagem pode ter pouco fundo disponível
- Tente usar imagens com mais área de fundo

## 📄 Licença

MIT License - veja o arquivo LICENSE para detalhes.

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para problemas ou dúvidas:

- Abra uma issue no GitHub
- Entre em contato via email: seu.email@exemplo.com

## 🔄 Changelog

### v1.0.0

- Versão inicial
- Interface gráfica PyQt5
- API programática completa
- Rotação e posicionamento aleatório
- Geração de fundos limpos

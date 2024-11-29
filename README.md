# ilab RAG ingestion pipeline
*E.g. how to overcome the current limitation of adding new commands to the `ilab` CLI v1.4 to ingest user documents for the RAG pipelines.*

## 1. Overview
To enable the ingestion of user documents and store them in a vector database for RAG pipelines, the following steps are involved:
1. Transform user documents into the `ilab` schema (using `docling` under the scenes) to generate pre-processed artifacts.
1. Generate embeddings from these pre-processed (JSON) artifacts and store them in a configured vector DB for use in the RAG pipeline.

## 2. Transforming user docs
Install `instructlab` dependencies, using one of the available options from the [installation sections](https://docs.instructlab.ai/) of the 
`InstructLab Project`. 

TLDR;)
```bash
pip install instructlab
```
Or, for MacOs:
```
pip install 'instructlab[mps]'
```

Use the provided Python script [prepare.py](./prepare.py) to convert documents from a local input folder to a destination folder.

In-line options can be used to override the default behavior. Environment variables can also be configured to hide the CLI options.
See the provided [.env](.env) file for an example of all the managed variables.
```bash
% python prepare.py --help
Usage: prepare.py [OPTIONS]

Options:
  --models-path TEXT  Path to the model. Overrides MODELS_PATH env variable or
                      default ilab configuration.
  --model-name TEXT   Model name. Overrides MODEL_NAME env variable or the
                      `generate.model` key from ilab configuration
  --input TEXT        Path of source documents. Overrides INPUT_DIR env
                      variable.
  --output TEXT       Path to transformed documents. Overrides OUTPUT_DIR env
                      variable or defaults to 'output'
  --help              Show this message and exit.
```

Example of command output:
```bash
% python prepare.py --input ./docs
Transforming ./docs to output using mistral-7b-instruct-v0.2.Q4_K_M.gguf from /Users/dmartino/.cache/instructlab/models
Transforming source files ['knowledge-wiki.pdf']
Tokenizer model is /Users/dmartino/.cache/instructlab/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
You are using the default legacy behaviour of the <class 'transformers.models.llama.tokenization_llama_fast.LlamaTokenizerFast'>. This is expected, and simply means that the `legacy` (previous) behavior will be used so nothing changes for you. If you want to use the new behaviour, set `legacy=False`. This should only be set if you understand what it means, and thoroughly read the reason why this was added as explained in https://github.com/huggingface/transformers/pull/24565 - if you loaded a llama tokenizer from a GGUF file you can ignore this message.
Merges were not in checkpoint, building merges on the fly.
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 32000/32000 [00:23<00:00, 1369.09it/s]
INFO 2024-11-29 11:18:53,192 instructlab.sdg.utils.chunkers:393: Successfully loaded tokenizer from: /Users/dmartino/.cache/instructlab/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
Created chunker <instructlab.sdg.utils.chunkers.ContextAwareChunker object at 0x17f6ebe50>
INFO 2024-11-29 11:18:54,575 instructlab.sdg.utils.chunkers:252: Docling models not found on disk, downloading models...
WARNING 2024-11-29 11:18:55,045 easyocr.easyocr:71: Using CPU. Note: This module is much faster with a GPU.
INFO 2024-11-29 11:18:58,028 docling.document_converter:211: Going to convert document batch...
WARNING 2024-11-29 11:18:58,030 easyocr.easyocr:71: Using CPU. Note: This module is much faster with a GPU.
INFO 2024-11-29 11:19:01,200 docling.pipeline.base_pipeline:37: Processing document knowledge-wiki.pdf
INFO 2024-11-29 11:19:02,858 docling.document_converter:228: Finished converting document knowledge-wiki.pdf in 5.26 sec.
INFO 2024-11-29 11:19:02,860 instructlab.sdg.utils.chunkers:652: Processed 1 docs, of which 0 failed
INFO 2024-11-29 11:19:02,860 instructlab.sdg.utils.chunkers:304: Processing parsed docling json file: output/docling-artifacts/knowledge-wiki.json
Created 1 chunks from 1 input documents
prepare() executed in 35.50 seconds.
```

## 3. Generate embeddings from pre-processed artifacts
**TODO**

## 4. Code management
Run the following to ensure the code is properly formatted and imports follow the standards:
```bash
pip install isort
ruff format .
isort .
```
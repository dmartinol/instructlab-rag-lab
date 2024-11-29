import os
import sys
import time
from pathlib import Path

import click
from dotenv import load_dotenv
from instructlab import configuration as cfg
from instructlab.defaults import DEFAULTS
from instructlab.sdg.utils.chunkers import DocumentChunker
from instructlab.utils import list_models

DEFAULT_OUTPUT_DIR = "output"

# Load environment variables from .env file
load_dotenv()


@click.command()
def dummy_command():
    pass


@click.command()
@click.option(
    "--models-path",
    default=None,
    help="Path to the model. Overrides MODELS_PATH env variable or default ilab configuration.",
)
@click.option(
    "--model-name",
    default=None,
    help="Model name. Overrides MODEL_NAME env variable or the `generate.model` key from ilab configuration ",
)
@click.option(
    "--input",
    default=None,
    help="Path of source documents. Overrides INPUT_DIR env variable.",
)
@click.option(
    "--output",
    default=None,
    help=f"Path to transformed documents. Overrides OUTPUT_DIR env variable or defaults to '{DEFAULT_OUTPUT_DIR}'",
)
def prepare(models_path, model_name, input, output):
    models_path, selected_model_name, input_dir, output_dir = _parse_arguments(
        models_path, model_name, input, output
    )
    start_time = time.time()
    _prepare(models_path, selected_model_name, input_dir, output_dir)
    print(f"prepare() executed in {time.time() - start_time:.2f} seconds.")


def _prepare(models_path, selected_model_name, input_dir, output_dir):
    print(
        f"Transforming {input_dir} to {output_dir} using {selected_model_name} from {models_path}"
    )

    source_files = _load_source_files(input_dir=input_dir)
    print(f"Transforming source files {[p.name for p in source_files]}")

    tokenizer_model_name = os.path.join(models_path, selected_model_name)
    print(f"Tokenizer model is {tokenizer_model_name}")

    chunker = DocumentChunker(
        leaf_node=_dummy_leaf_node(source_files),
        taxonomy_path=output_dir,
        output_dir=output_dir,
        tokenizer_model_name=tokenizer_model_name,
    )
    print(f"Created chunker {chunker}")
    chunks = chunker.chunk_documents()
    print(f"Created {len(chunks)} chunks from {len(source_files)} input documents")


def _parse_arguments(models_path, model_name, input, output) -> tuple:
    models_path = models_path or os.getenv("MODELS_PATH") or DEFAULTS.MODELS_DIR
    if not Path(models_path).exists() or not Path(models_path).is_dir():
        sys.exit(f"Models path {models_path} does not exist or not a dir")

    default_model_name = Path(cfg.get_default_config().generate.model).name
    selected_model_name = model_name or os.getenv("MODEL_NAME") or default_model_name
    available_models = list_models([Path(DEFAULTS.MODELS_DIR)], True)
    exists = any(entry[0] == selected_model_name for entry in available_models)
    if not exists:
        sys.exit(
            f"selected model name {selected_model_name} not found. Available models are {[m[0] for m in available_models]}"
        )

    input_dir = input or os.getenv("INPUT_DIR")
    if not input_dir:
        sys.exit("Missing required option input_dir")
    if not Path(input_dir).exists() or not Path(input_dir).is_dir():
        sys.exit(f"Input folder {input_dir} does not exist or not a dir")

    output_dir = output or os.getenv("OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    if not output_dir:
        sys.exit("Missing required option output_dir")
    if Path(output_dir).exists() and not Path(output_dir).is_dir():
        sys.exit(f"Output folder {output_dir} is not a dir")
    if not Path(output_dir).exists():
        os.makedirs(output_dir, exist_ok=True)

    return models_path, selected_model_name, input_dir, output_dir


def _load_source_files(input_dir) -> list[Path]:
    return [Path(os.path.join(input_dir, f)) for f in os.listdir(input_dir)]


def _dummy_leaf_node(source_files):
    return [
        {
            "documents": ["not relevant"],
            "taxonomy_path": "not relevant",
            "filepaths": source_files,
        }
    ]


if __name__ == "__main__":
    cfg.init(click.Context(dummy_command), cfg.DEFAULTS.CONFIG_FILE)
    prepare()

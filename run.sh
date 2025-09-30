slide="slides/slide_${1-00}"*".py"
pyright $slide && uv run $slide

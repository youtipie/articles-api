from .articles import spec as articles_spec
from .articles_with_id import spec as articles_with_id_spec

spec = {
    "/article": articles_spec,
    "/article/{article_id}": articles_with_id_spec
}

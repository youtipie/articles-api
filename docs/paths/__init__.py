from .auth import spec as auth_spec
from .users import spec as users_spec
from .article import spec as article_spec

spec = {
    **auth_spec,
    **users_spec,
    **article_spec
}

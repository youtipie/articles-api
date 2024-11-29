from .roles import spec as roles_spec
from .users import spec as users_spec
from .users_with_id import spec as users_with_id_spec

spec = {
    "/users/roles": roles_spec,
    "/users": users_spec,
    "/users/{user_id}": users_with_id_spec
}

#include "custom/dependencies.hpp"

#include <userver/components/component_config.hpp>
#include <userver/components/component_context.hpp>

namespace custom {

namespace {} // namespace

Dependencies::Dependencies(const components::ComponentConfig & /*config*/,
                           const components::ComponentContext &context)
    : network_users_client(
          context.FindComponent<
              custom_clients::network_users::NetworkUsersClient>()) {}

}; // namespace custom

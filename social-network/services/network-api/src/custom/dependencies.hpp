#pragma once

#include <userver/components/component_fwd.hpp>

#include <clients/network_users_client.hpp>

namespace custom {

namespace {
namespace components = userver::components;
}

class Dependencies {
public:
  Dependencies(const components::ComponentConfig &,
               const components::ComponentContext &);

  Dependencies(Dependencies &&) = delete;
  Dependencies operator=(Dependencies &&) = delete;
  
  custom_clients::network_users::NetworkUsersClient &network_users_client;
};

} // namespace custom

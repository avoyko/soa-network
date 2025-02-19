#pragma once

#include <userver/components/component.hpp>
#include <userver/components/component_context.hpp>

#include <userver/clients/dns/component.hpp>
#include <userver/clients/http/component.hpp>
#include <userver/clients/http/response.hpp>
#include <userver/yaml_config/merge_schemas.hpp>

namespace custom_clients::network_users {

namespace {

using ResponsePtr = std::shared_ptr<userver::clients::http::Response>;

} // namespace

class NetworkUsersClient : public userver::components::ComponentBase {
public:
  static constexpr std::string_view kName = "network-users-client";

  NetworkUsersClient(const userver::components::ComponentConfig &config,
                     const userver::components::ComponentContext &context);

  ResponsePtr V1Login(std::string action) const;

  ResponsePtr V1Signup(std::string action) const;

  ResponsePtr V1UpdateProfile(std::string action) const;

  ResponsePtr V1ProfileInfo(std::string action) const;

  static userver::yaml_config::Schema GetStaticConfigSchema() {
    return userver::yaml_config::MergeSchemas<
        userver::components::ComponentBase>(R"(
    type: object
    description: HTTP client for network-users service
    additionalProperties: false
    properties:
      service-url:
          type: string
          description: URL of the service to send the actions to
    )");
  }

private:
  const std::string service_url_;
  userver::clients::http::Client &http_client_;
};

} // namespace custom_clients::network_users
#include "network_users_client.hpp"

namespace custom_clients::network_users {
namespace {

namespace components = userver::components;

constexpr auto kLoginUrl = "/v1/login";
constexpr auto kSignupUrl = "/v1/signup";
constexpr auto kUpdateProfileUrl = "/v1/update-profile";
constexpr auto kProfileInfoUrl = "/v1/profile-info";

} // namespace

NetworkUsersClient::NetworkUsersClient(
    const components::ComponentConfig &config,
    const components::ComponentContext &context)
    : ComponentBase{config, context},
      service_url_(config["service-url"].As<std::string>()),
      http_client_(
          context.FindComponent<components::HttpClient>().GetHttpClient()) {}

ResponsePtr NetworkUsersClient::V1Login(std::string action) const {
  return http_client_.CreateRequest()
      .url(service_url_)
      .post(fmt::format("{}{}", service_url_, kLoginUrl))
      .data(std::move(action))
      .perform();
}

ResponsePtr NetworkUsersClient::V1Signup(std::string action) const {
  return http_client_.CreateRequest()
      .url(service_url_)
      .post(fmt::format("{}{}", service_url_, kSignupUrl))
      .data(std::move(action))
      .perform();
}

ResponsePtr NetworkUsersClient::V1UpdateProfile(std::string action) const {
  return http_client_.CreateRequest()
      .url(service_url_)
      .post(fmt::format("{}{}", service_url_, kUpdateProfileUrl))
      .data(std::move(action))
      .perform();
}

ResponsePtr NetworkUsersClient::V1ProfileInfo(std::string action) const {
  return http_client_.CreateRequest()
      .url(service_url_)
      .get(fmt::format("{}{}", service_url_, kProfileInfoUrl))
      .data(std::move(action))
      .perform();
}

} // namespace custom_clients::network_users
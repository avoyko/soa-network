#include "network_users.hpp"

#include <custom/dependencies.hpp>
#include <userver/server/http/http_method.hpp>

namespace fetchers {

std::string
LoginUser(userver::server::http::HttpRequest &request,
          userver::server::request::RequestContext &context,
          custom_clients::network_users::NetworkUsersClient &client) {
  auto response = client.V1Login(request.ExtractRequestBody());
  return response->sink_string();
}

std::string
SignupUser(userver::server::http::HttpRequest &request,
           userver::server::request::RequestContext &context,
           custom_clients::network_users::NetworkUsersClient &client) {
  auto response = client.V1Signup(request.ExtractRequestBody());
  return response->sink_string();
}

std::string
UpdateUserProfile(userver::server::http::HttpRequest &request,
                  userver::server::request::RequestContext &context,
                  custom_clients::network_users::NetworkUsersClient &client) {
  auto response = client.V1UpdateProfile(request.ExtractRequestBody());
  return response->sink_string();
}

std::string
GetUserProfileInfo(userver::server::http::HttpRequest &request,
                   userver::server::request::RequestContext &context,
                   custom_clients::network_users::NetworkUsersClient &client) {
  auto response = client.V1ProfileInfo(request.ExtractRequestBody());
  return response->sink_string();
}

} // namespace fetchers
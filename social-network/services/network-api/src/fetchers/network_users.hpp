#pragma once

#include "clients/network_users_client.hpp"
#include <userver/http/common_headers.hpp>
#include <userver/server/handlers/http_handler_base.hpp>

namespace fetchers {

std::string
LoginUser(userver::server::http::HttpRequest &request,
          userver::server::request::RequestContext &context,
          custom_clients::network_users::NetworkUsersClient &client);

std::string
GetUserProfileInfo(userver::server::http::HttpRequest &request,
                   userver::server::request::RequestContext &context,
                   custom_clients::network_users::NetworkUsersClient &client);

std::string
SignupUser(userver::server::http::HttpRequest &request,
           userver::server::request::RequestContext &context,
           custom_clients::network_users::NetworkUsersClient &client);

std::string
UpdateUserProfile(userver::server::http::HttpRequest &request,
                  userver::server::request::RequestContext &context,
                  custom_clients::network_users::NetworkUsersClient &client);

} // namespace fetchers
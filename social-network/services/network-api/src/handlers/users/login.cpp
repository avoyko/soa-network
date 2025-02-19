
#include "login.hpp"

#include <userver/http/common_headers.hpp>
#include <userver/server/handlers/http_handler_base.hpp>

#include <fetchers/network_users.hpp>

namespace handlers::users::login {

UsersLoginHandler::UsersLoginHandler(
    const userver::components::ComponentConfig &config,
    const userver::components::ComponentContext &context)
    : userver::server::handlers::HttpHandlerBase(config, context),
      dependencies_(std::make_unique<custom::Dependencies>(config, context)) {};

std::string UsersLoginHandler::HandleRequest(
    userver::server::http::HttpRequest &request,
    userver::server::request::RequestContext &context) const {
  return fetchers::LoginUser(request, context,
                             dependencies_->network_users_client);
}

} // namespace handlers::users::login

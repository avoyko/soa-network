#include "update_profile.hpp"

#include <userver/http/common_headers.hpp>
#include <userver/server/handlers/http_handler_base.hpp>

#include <fetchers/network_users.hpp>

namespace handlers::users::update_profile {

UsersUpdateProfileHandler::UsersUpdateProfileHandler(
    const userver::components::ComponentConfig &config,
    const userver::components::ComponentContext &context)
    : userver::server::handlers::HttpHandlerBase(config, context),
      dependencies_(std::make_unique<custom::Dependencies>(config, context)) {};

std::string UsersUpdateProfileHandler::HandleRequest(
    userver::server::http::HttpRequest &request,
    userver::server::request::RequestContext &context) const {
  return fetchers::UpdateUserProfile(request, context,
                                     dependencies_->network_users_client);
}

} // namespace handlers::users::update_profile

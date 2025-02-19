#pragma once

#include <custom/dependencies.hpp>
#include <userver/http/common_headers.hpp>
#include <userver/server/handlers/http_handler_base.hpp>

#include <schemas/handlers/users/profile_info_fwd.hpp>

namespace handlers::users::profile_info {

class UsersProfileInfoHandler final
    : public userver::server::handlers::HttpHandlerBase {
public:
  static constexpr std::string_view kName = "handler-users-profile-info";

  using HttpHandlerBase::HttpHandlerBase;

  UsersProfileInfoHandler(const userver::components::ComponentConfig &config,
                          const userver::components::ComponentContext &context);

  std::string
  HandleRequest(userver::server::http::HttpRequest &request,
                userver::server::request::RequestContext &) const override;

private:
  std::unique_ptr<custom::Dependencies> dependencies_;
};

} // namespace handlers::users::profile_info

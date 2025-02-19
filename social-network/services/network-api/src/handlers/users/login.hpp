#pragma once

#include <custom/dependencies.hpp>
#include <userver/http/common_headers.hpp>
#include <userver/server/handlers/http_handler_base.hpp>

namespace handlers::users::login {

class UsersLoginHandler final
    : public userver::server::handlers::HttpHandlerBase {
public:
  static constexpr std::string_view kName = "handler-users-login";

  using HttpHandlerBase::HttpHandlerBase;

  UsersLoginHandler(const userver::components::ComponentConfig &config,
                    const userver::components::ComponentContext &context);

  std::string HandleRequest(
      userver::server::http::HttpRequest &request,
      userver::server::request::RequestContext &context) const override;

private:
  std::unique_ptr<custom::Dependencies> dependencies_;
};

} // namespace handlers::users::login

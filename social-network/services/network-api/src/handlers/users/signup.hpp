#pragma once

#include <custom/dependencies.hpp>
#include <userver/components/component_list.hpp>
#include <userver/server/handlers/http_handler_base.hpp>

namespace handlers::users::signup {

class UsersSignupHandler final
    : public userver::server::handlers::HttpHandlerBase {
public:
  static constexpr std::string_view kName = "handler-users-signup";

  using HttpHandlerBase::HttpHandlerBase;

  UsersSignupHandler(const userver::components::ComponentConfig &config,
                     const userver::components::ComponentContext &context);

  std::string
  HandleRequest(userver::server::http::HttpRequest &request,
                userver::server::request::RequestContext &) const override;

private:
  std::unique_ptr<custom::Dependencies> dependencies_;
};

} // namespace handlers::users::signup

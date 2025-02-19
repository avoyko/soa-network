
#include <userver/clients/dns/component.hpp>
#include <userver/components/minimal_server_component_list.hpp>
#include <userver/utils/daemon_run.hpp>

#include <handlers/users/login.hpp>
#include <handlers/users/profile_info.hpp>
#include <handlers/users/signup.hpp>
#include <handlers/users/update_profile.hpp>

#include <clients/network_users_client.hpp>

int main(int argc, char *argv[]) {
  auto component_list =
      userver::components::MinimalServerComponentList()
          .Append<handlers::users::login::UsersLoginHandler>()
          .Append<handlers::users::profile_info::UsersProfileInfoHandler>()
          .Append<handlers::users::signup::UsersSignupHandler>()
          .Append<handlers::users::update_profile::UsersUpdateProfileHandler>()
          .Append<custom_clients::network_users::NetworkUsersClient>()
          .Append<userver::components::HttpClient>()
          .Append<userver::clients::dns::Component>();
  return userver::utils::DaemonMain(argc, argv, component_list);
}

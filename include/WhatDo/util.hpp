#pragma once

#include <nlohmann/json.hpp>

#include <vector>

namespace util {
enum choosable { steam, battlenet, epic, misc, task, Uni };

std::vector<nlohmann::json> get_games(const choosable art);
nlohmann::json* choose(const std::vector<nlohmann::json*>& choose);
void save_games(const choosable e, const std::vector<nlohmann::json>& s);

namespace steamutils {

std::string get_steam_store_link(int app_id);
int update_steam_games();

}  // namespace steamutils
}  // namespace util

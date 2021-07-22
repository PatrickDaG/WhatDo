#pragma once

#include <nlohmann/json.hpp>

#include <vector>

namespace util {
enum choosable { steam, battlenet, epic, misc, task, Uni };

std::vector<nlohmann::json> get_games(choosable art);
nlohmann::json* choose(std::vector<nlohmann::json*> choose);
void save_games(const choosable e, std::vector<nlohmann::json> s);

namespace steamu {

std::string get_steam_store_link(int app_id);
int update_steam_games();

}  // namespace steam
}  // namespace util

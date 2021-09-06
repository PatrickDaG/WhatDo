#include <WhatDo/util.hpp>
#include <cpr/cpr.h>
#include <nlohmann/json.hpp>
#include <magic_enum.hpp>
#include <fmt/format.h>
#include <optional>

#include <iostream>
#include <fstream>
#include <set>
#include <string>
#include <random>
#include <vector>

namespace util {

namespace steamutils {

struct steam_game_compare {
	bool operator()(const nlohmann::json& l, const nlohmann::json& r) const {
		return l.at("appid").get<int>() < r.at("appid").get<int>();
	}
};

std::optional<nlohmann::json> fetch_steam_games() {
	cpr::Url url("https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/");
	cpr::Parameters para{{"key", "1055516A5F304C1CCACEA63BF42053C3"},
	                     {"steamid", "76561198060162001"},
	                     {"include_played_free_games", "true"},
	                     {"include_appinfo", "true"}};

	cpr::Response r = cpr::Get(url, para);
	if(r.text.empty())
		return std::nullopt;
	return nlohmann::json::parse(r.text).at("response");
}

int update_steam_games() {
	auto web_opt = fetch_steam_games();

	if(not web_opt) {
		fmt::print("Error fetching steam games");
		return 0;
	}
	auto web = web_opt.value();

	nlohmann::json local;
	std::fstream in("./data/games/steam.json", std::ios::in | std::ios::out);
	in >> local;
	auto local_games = local.at("games").get<std::set<nlohmann::json, steam_game_compare>>();

	local_games.merge(web.at("games").get<std::set<nlohmann::json>>());

	int ret = web.at("game_count").get<int>() - local.at("game_count").get<int>();
	local.at("game_count") = web.at("game_count").get<int>();
	local.at("games") = local_games;

	in.seekg(std::ios::beg);
	in << local.dump(4);
	return ret;
}

std::string get_steam_store_link(int app_id) { return fmt::format("https://store.steampowered.com/app/{}", app_id); }

}  // namespace steamutils

std::vector<nlohmann::json> get_games(const choosable art) {
	nlohmann::json j;
	std::string filename = fmt::format("./data/games/{}.json", magic_enum::enum_name(art));
	std::ifstream in(filename, std::ios::in);
	in >> j;
	return j.at("games").get<std::vector<nlohmann::json>>();
}

void save_games(const choosable e, const std::vector<nlohmann::json>& s) {
	nlohmann::json j{{"game_count", s.size()}, {"games", s}};
	auto filename = fmt::format("./data/games/{}.json", magic_enum::enum_name(e));
	std::ofstream out(filename, std::ios::out);
	out << j.dump(4);
}

int get_rand_num(const int min, const int max) {
	std::random_device r;
	std::default_random_engine eng(r());
	std::uniform_int_distribution<int> dist(min, max);
	return dist(eng);
}

nlohmann::json* choose(const std::vector<nlohmann::json*>& choose) {
	const int count = choose.size();
	int rand = get_rand_num(0, count - 1);
	return choose[rand];
}

}  // namespace util

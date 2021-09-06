#include <WhatDo/cli.hpp>
#include <cstdlib>
#include <iostream>
#include <vector>
#include <utility>
#include <fmt/core.h>

namespace cli {
cli::cli() : items{} {
	fmt::print("Added {} new steam games\n", util::steamutils::update_steam_games());
	items.emplace(std::make_pair(util::choosable::steam, util::get_games(util::choosable::steam)));
}

cli::~cli() {
	for(const auto& [k, v] : items) util::save_games(k, v);
}

nlohmann::json* cli::choose_all() {
	std::vector<nlohmann::json*> all;
	for(auto& [k, v] : items) {
		for(auto& i : v) {
			if((not i.contains("exclude") or i.at("exclude") == false) and
			   (not i.contains("completed") or i.at("completed") == false))
				all.emplace_back(&i);
		}
	}
	return util::choose(all);
}

int start() {
	cli c;
	while(true) {
		auto cur = c.choose_all();
		fmt::print("Current game: {}\n", cur->at("name"));
		fmt::print("{}\n", util::steamutils::get_steam_store_link(cur->at("appid")));
		fmt::print("(r) for redraw, (e) for exclude, (c) for completed, (exit) for exit)\n");
		std::string in;
		std::getline(std::cin, in);
		if(in.compare("r") == 0) {
			continue;
		} else if(in.compare("e") == 0) {
			(*cur)["exclude"] = true;
			continue;
		} else if(in.compare("c")) {
			(*cur)["completed"] = true;
		} else if(in.compare("exit") == 0) {
			return EXIT_SUCCESS;
		}
	}
}
}  // namespace cli

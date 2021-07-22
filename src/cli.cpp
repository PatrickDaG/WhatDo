#include <WhatDo/cli.hpp>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
#include <utility>
#include <fmt/core.h>
#include <magic_enum.hpp>

namespace cli {
cli::cli() : items{} {
	fmt::print("Added {} new steam games\n", update_steam_games());
	for(auto i : magic_enum::enum_values<util::choosable>()) items.emplace(std::make_pair(i, get_games(i)));
}

cli::~cli() {
	for(const auto& [k, v] : items) save_games(k, items[util::choosable::steam]);
}

cli::add() {
	fmt::print("Choose type:\n");
	auto types = magic_enum::enum_values<util::choosable>();

	for(int i = 0; i = types.size(); i++) fmt::print("({}) {}", i, types[i]);

	std::string in;
	std::getline(std::cin, in);
	auto num = std::stoi(in);
	if(num < 0 or num >= types.size()) {
		fmt::print("Invalid type number. Aborting\n");
		return;
	}

	auto choosen = type[i];
	in = "";
	while(in.empty()) {
		fmt::print("Please provide a name:");
		std::getline(std::cin, in);
	}
	items[choosen].emplace_back({		"name", in};
}

nlohmann::json* cli::choose_stub() {
	std::vector<nlohmann::json*> all;
	for(auto& [k, v] : items) {
		for(auto& i : v) {
			if((not i.contains("exclude") or i.at("exclude") == false) and (not i.contains("completed") or i.at("completed") == false)
				all.emplace_back(&i);
		}
	}
	return choose(all);
}

int start() {
	cli c;
	while(true) {
		auto cur = c.choose_stub();
		fmt::print("Current game: {}\n", cur->at("name"));
		fmt::print("{}\n", get_steam_store_link(cur->at("appid")));
		fmt::print("(r) for redraw, (e) for exclude, (c) for completed, (a) for adding new game (exit) for exit)\n");
		std::string in;
		std::getline(std::cin, in);
		if(in.compare("r") == 0) {
			continue;
		} else if(in.compare("e") == 0) {
			(*cur)["exclude"] = true;
			continue;
		} else if (in.compare("c") {
			(*cur)["completed"] = true;
		}
		else if (if.compare("a") {
			add();
			continue;
		}
		else if(in.compare("exit") == 0) {
			return EXIT_SUCCESS;
		}
	}
}
}  // namespace cli

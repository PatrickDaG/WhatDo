#pragma once

#include <WhatDo/util.hpp>
#include <nlohmann/json.hpp>

#include <unordered_map>
#include <vector>

namespace cli {

class cli {
private:
	std::unordered_map<choosable, std::vector<nlohmann::json>> items;

public:
	nlohmann::json* choose_all();

	cli();
	~cli();
};

int start();

}  // namespace cli

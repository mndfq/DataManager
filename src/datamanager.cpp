#include "datamanager.h"
#include <fstream>
#include <sstream>

bool DataManager::load(const std::string& filename)
{
	std::ifstream in(filename);
	if (!in.is_open()) return false;

	data_.clear();
	std::string line;
	while (std::getline(in, line)) 
	{
		if (line.empty() || line[0] == '#') continue;
		std::istringstream iss(line);
		std::string key, value;
		if (std::getline(iss, key, '=') && std::getline(iss, value))
		{
			data_[key] = value;
		}
	}
	return true;
}
bool DataManager::save(const std::string& filename) const
{
	std::ofstream out(filename);
	if (!out.is_open()) return false;

	for (const auto& [key, value] : data_)
	{
		out << key << "=" << value << "\n";
	}
	return true;
}

void DataManager::set(const std::string& key, const std::string& value)
{
	data_[key] = value;
}

std::string DataManager::get(const std::string& key, const std::string& defaultValue) const
{
	auto it = data_.find(key);
	return (it != data_.end()) ? it -> second : defaultValue;
}

bool DataManager::remove(const std::string& key) {
    return data_.erase(key) > 0;
}

bool DataManager::exists(std::string& key) const {
    return data_.find(key) != data_.end();
}

std::vector<std::string> DataManager::keys() const
{
	std::vector<std::string> ks;
	ks.reserve(data_.size());
	for (const auto& [key, _] : data_)
	{
		ks.push_back(key);
	}
	return ks;
}

void DataManager::clear()
{
	data_.clear();
}

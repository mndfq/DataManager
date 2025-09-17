#ifndef DATAMANAGER_H
#define DATAMANAGER_H

#include <string>
#include <vector>
#include <unordered_map>

class DataManager
{
	public:
		// File Operations
		bool load(const std::string& filename);
		bool save(const std::string& filename) const;
		// CRUD Operations
		void set(const std::string& key, const std::string& value);
		std::string get(const std::string& key, const std::string& defaultValue = "") const;
		bool remove(const std::string& key);
		// Other Operations
		bool exists(std::string& key) const;
		std::vector<std::string> keys() const;
		void clear();
	private:
		std::unordered_map<std::string, std::string> data_;
};
#endif

#include "game.h"
#include <string>
#include <fstream>


Game::Game(std::string player1_name, std::string player2_name) : 
player1_score(0), player2_score(0), player1_name(player1_name), player2_name(player2_name) {}

void Game::playRound(int player1_choice, int player2_choice) {
    round_history.emplace_back(player1_choice, player2_choice);
    if (player1_choice == player2_choice) {
        player1_score += player1_choice;
        player2_score += player2_choice;
    } 
    else if (abs(player1_choice - player2_choice) > 1) {
        player1_score += player1_choice;
        player2_score += player2_choice;
    } 
    else if (abs(player1_choice - player2_choice) == 1) {
        int sum = player1_choice + player2_choice;
        if (player1_choice < player2_choice) {
            player1_score += sum;
        } else {
            player2_score += sum;
        }
    }
}


std::pair<int, int> Game::getScores() const {
    return {player1_score, player2_score};
}


const std::vector<std::pair<int, int>>& Game::getRoundHistory() const {
    return round_history;
}


void Game::setPlayerName(std::string player1_name, std::string player2_name) { 
    this->player1_name = player1_name; 
    this->player2_name = player2_name; 
    }


void Game::saveGameToFile(const std::string& filename) const {
    std::ofstream file(filename);  // Відкриваємо файл для запису
    if (!file.is_open()) {
        throw std::runtime_error("Unable to open file for writing!");
    }

    file << "Історія гри\n";
    file << "-----------------------------------------\n";
    for (size_t round = 0; round < round_history.size(); ++round) {
        file << round + 1 << ". " 
             << player1_name << " - " << round_history[round].first
             << "   |   " 
             << player2_name << " - " << round_history[round].second 
             << "\n";
    }
    file.close();  // Закриваємо файл
}


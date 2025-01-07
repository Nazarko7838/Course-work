#ifndef GAME_H
#define GAME_H

#include <vector>
#include <utility>
#include <string>

class Game {
public:
    Game(std::string player1_name, std::string player2_name);
    void playRound(int player1_choice, int player2_choice);
    void setPlayerName(std::string player1_name, std::string player2_name);
    void saveGameToFile(const std::string& filename) const;
    std::pair<int, int> getScores() const;
    const std::vector<std::pair<int, int>>& getRoundHistory() const;

private:
    std::string player1_name;
    std::string player2_name;
    int player1_score;
    int player2_score;
    std::vector<std::pair<int, int>> round_history;
};

#endif // GAME_H

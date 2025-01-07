#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "game.h"

namespace py = pybind11;

PYBIND11_MODULE(game_module, m) {
    py::class_<Game>(m, "Game")
        .def(py::init<std::string, std::string>(), py::arg("player1_name"), py::arg("player2_name"))
        .def("playRound", &Game::playRound)
        .def("getScores", &Game::getScores)
        .def("getRoundHistory", &Game::getRoundHistory)
        .def("saveGameToFile", &Game::saveGameToFile)
        ;
}

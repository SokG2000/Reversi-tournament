#include <iostream>

using namespace std;

const int WHITE = 0;
const int BLACK = 1;
const int EMPTY = -1;
const int board_sz = 8;
const int num_dirs = 8;

void read_position(int board[board_sz][board_sz], int* turn) {
    cin >> *turn;
    for (int i = 0; i < board_sz; ++i) {
        for (int j = 0; j < board_sz; ++j) {
            cin >> board[i][j];
        }
    }
}

int count_reversed(int board[board_sz][board_sz], int x, int y, int player) {
    if (x < 0 || x >= board_sz || y < 0 || y >= board_sz) {
        return 0;
    }
    if (board[x][y] != EMPTY) {
        return 0;
    }
    int DX[] = {-1, 0, 1, 1, 1, 0, -1, -1};
    int DY[] = {1, 1, 1, 0, -1, -1, -1, 0};
    int reversed = 0;
    for (int i = 0; i < num_dirs; ++i) {
        int dx = DX[i];
        int dy = DY[i];
        int nx = x + dx;
        int ny = y + dy;
        int direction_reversed = 0;
        while (nx >= 0 && nx < board_sz && ny >= 0 && ny < board_sz && board[nx][ny] == 1 - player) {
            ++direction_reversed;
            nx += dx;
            ny += dy;
        }
        if (nx >= 0 && nx < board_sz && ny >= 0 && ny < board_sz && board[nx][ny] == player && direction_reversed > 0) {
            reversed += direction_reversed;
        }
    }
    return reversed;
}

bool can_move(int board[board_sz][board_sz], int x, int y, int player) {
    return count_reversed(board, x, y, player) > 0;
}

pair <int, int> easy_choise(int board[board_sz][board_sz], int player) {
    pair <int, int> best_pair = make_pair(-1, -1);
    int best_score = 0;
    for (int x = 0; x < board_sz; ++x) {
        for (int y = 0; y < board_sz; ++y) {
            int score = count_reversed(board, x, y, player);
            if (score > best_score) {
                best_pair = make_pair(x, y);
                best_score = score;
            }
        }
    }
    return best_pair;
}

int num_black(int board[board_sz][board_sz]) {
    int res = 0;
    for (int i = 0; i < board_sz; ++i) {
        for (int j = 0; j < board_sz; ++j) {
            if (board[i][j] == BLACK) {
                ++res;
            }
        }
    }
    return res;
}

int main() {
    int board[board_sz][board_sz];
    int turn;
    read_position(board, &turn);
    pair <int, int> decision = easy_choise(board, turn);
    cout << decision.first << " " << decision.second << "\n";
    return 0;
}


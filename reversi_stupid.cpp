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

bool can_move(int board[board_sz][board_sz], int x, int y, int player) {
    if (x < 0 || x >= board_sz || y < 0 || y >= board_sz) {
        return false;
    }
    if (board[x][y] != EMPTY) {
        return false;
    }
    int DX[] = {-1, 0, 1, 1, 1, 0, -1, -1};
    int DY[] = {1, 1, 1, 0, -1, -1, -1, 0};
    for (int i = 0; i < num_dirs; ++i) {
        int dx = DX[i];
        int dy = DY[i];
        int nx = x + dx;
        int ny = y + dy;
        int reversed = 0;
        while (nx >= 0 && nx < board_sz && ny >= 0 && ny < board_sz && board[nx][ny] == 1 - player) {
            ++reversed;
            nx += dx;
            ny += dy;
        }
        if (nx >= 0 && nx < board_sz && ny >= 0 && ny < board_sz && board[nx][ny] == player && reversed > 0) {
            return true;
        }
    }
    return false;
}

pair <int, int> stupid_choise(int board[board_sz][board_sz], int player) {
    for (int x = 0; x < board_sz; ++x) {
        for (int y = 0; y < board_sz; ++y) {
            if (can_move(board, x, y, player)) {
                return make_pair(x, y);
            }
        }
    }
    return make_pair(-1, -1);
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
    pair <int, int> decision = stupid_choise(board, turn);
    cout << decision.first << " " << decision.second << "\n";
    return 0;
}


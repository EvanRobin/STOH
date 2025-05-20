#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define L 40
#define EMPTY -1
#define TREE 1
#define FIRE 0

int grid[L][L];
int new_grid[L][L];

// Random float between 0 and 1
float randf() {
    return rand() / (float)RAND_MAX;
}

// Initialize grid
void initialize_grid(float p, float f) {
    for (int i = 0; i < L; i++) {
        for (int j = 0; j < L; j++) {
            if (randf() < p) {
                if (randf() < f)
                    grid[i][j] = FIRE;
                else
                    grid[i][j] = TREE;
            } else {
                grid[i][j] = EMPTY;
            }
        }
    }
}

// Count current fires
int count_fires() {
    int fires = 0;
    for (int i = 0; i < L; i++)
        for (int j = 0; j < L; j++)
            if (grid[i][j] == FIRE)
                fires++;
    return fires;
}

// Update grid
void update_grid(float g) {
    for (int i = 0; i < L; i++) {
        for (int j = 0; j < L; j++) {
            int up    = grid[(i - 1 + L) % L][j];
            int down  = grid[(i + 1) % L][j];
            int left  = grid[i][(j - 1 + L) % L];
            int right = grid[i][(j + 1) % L];

            if (grid[i][j] == FIRE) {
                new_grid[i][j] = EMPTY;
            } else if (grid[i][j] == TREE &&
                       (up == FIRE || down == FIRE || left == FIRE || right == FIRE)) {
                new_grid[i][j] = FIRE;
            } else if (grid[i][j] == EMPTY && randf() < g) {
                new_grid[i][j] = TREE;
            } else {
                new_grid[i][j] = grid[i][j];
            }
        }
    }

    // Copy new grid back
    for (int i = 0; i < L; i++)
        for (int j = 0; j < L; j++)
            grid[i][j] = new_grid[i][j];
}

// Simulate fire spread
int forest_fire(float g, int max_steps) {
    int steps = 0;
    for (int t = 0; t < max_steps; t++) {
        if (count_fires() == 0)
            break;
        update_grid(g);
        steps++;
    }
    return steps;
}

// Eternal flame function
float eternal_flame(float start_g, float max_g, float step_g, int max_steps) {
    for (float g = start_g; g < max_g; g += step_g) {
        initialize_grid(0.6f, 0.1f);
        if (forest_fire(g, max_steps) == max_steps) {
            return g;
        }
    }
    return max_g;
}

int main() {
    srand(time(NULL));
    float g_found = eternal_flame(0.082f, 0.1f, 0.001f, 1000000000);
    printf("Eternal flame reached at g = %.5f\n", g_found);
    return 0;
}

/*
Eternal flame reached at g = 0.07900
Eternal flame reached at g = 0.08100
Eternal flame reached at g = 0.08000
Eternal flame reached at g = 0.08000
Eternal flame reached at g = 0.08200
Eternal flame reached at g = 0.08200
Eternal flame reached at g = 0.08200 
Eternal flame reached at g = 0.08200 
Eternal flame reached at g = 0.08200 
Eternal flame reached at g = 0.08200  
Eternal flame reached at g = 0.08200 
*/

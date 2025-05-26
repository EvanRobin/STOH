#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define L 40
#define TREE 1
#define EMPTY -1
#define FIRE 0
#define STEPS 1000
#define RUNS 10

double p = 0.6;     // Starting tree probability
double f = 0.1;     // Fire probability
double g = 0.082;   // Tree growth probability

int grid[L][L];
int new_grid[L][L];

// Random double in [0,1]
double rand_double() {
    return (double)rand() / RAND_MAX;
}

// Initialize grid
void initialize_grid() {
    for (int i = 0; i < L; i++) {
        for (int j = 0; j < L; j++) {
            grid[i][j] = (rand_double() < p) ? TREE : EMPTY;
            if (grid[i][j] == TREE && rand_double() < f)
                grid[i][j] = FIRE;
        }
    }
}

// Update grid
void update_grid() {
    for (int i = 0; i < L; i++) {
        for (int j = 0; j < L; j++) {
            int fire_neighbor = 0;
            if (grid[(i + 1) % L][j] == FIRE) fire_neighbor++;
            if (grid[(i - 1 + L) % L][j] == FIRE) fire_neighbor++;
            if (grid[i][(j + 1) % L] == FIRE) fire_neighbor++;
            if (grid[i][(j - 1 + L) % L] == FIRE) fire_neighbor++;

            if (grid[i][j] == FIRE) {
                new_grid[i][j] = EMPTY;
            } else if (grid[i][j] == EMPTY && rand_double() < g) {
                new_grid[i][j] = TREE;
            } else if (grid[i][j] == TREE && fire_neighbor > 0) {
                new_grid[i][j] = FIRE;
            } else {
                new_grid[i][j] = grid[i][j];
            }
        }
    }

    // Copy back to grid
    for (int i = 0; i < L; i++)
        for (int j = 0; j < L; j++)
            grid[i][j] = new_grid[i][j];
}

// Simple flood fill to count clusters
int visited[L][L];

int flood_fill(int x, int y, int label) {
    if (x < 0 || x >= L || y < 0 || y >= L || grid[x][y] != FIRE || visited[x][y])
        return 0;

    visited[x][y] = label;

    int size = 1;
    size += flood_fill((x + 1) % L, y, label);
    size += flood_fill((x - 1 + L) % L, y, label);
    size += flood_fill(x, (y + 1) % L, label);
    size += flood_fill(x, (y - 1 + L) % L, label);

    return size;
}

// Analyze fire clusters
void analyze_fire_clusters(int *cluster_sizes, int *total_clusters) {
    for (int i = 0; i < L; i++)
        for (int j = 0; j < L; j++)
            visited[i][j] = 0;

    int label = 1;
    *total_clusters = 0;

    for (int i = 0; i < L; i++) {
        for (int j = 0; j < L; j++) {
            if (grid[i][j] == FIRE && visited[i][j] == 0) {
                int size = flood_fill(i, j, label++);
                if (size > 0 && *total_clusters < 10000)
                    cluster_sizes[(*total_clusters)++] = size;
            }
        }
    }
}

int main() {
    srand(time(NULL));

    for (int run = 0; run < RUNS; run++) {
        initialize_grid();

        int cluster_sizes[1000000];
        int total_sizes = 0;

        for (int step = 0; step < STEPS; step++) {
            update_grid();
            int fire_clusters[10000], num_clusters;
            analyze_fire_clusters(fire_clusters, &num_clusters);
            for (int i = 0; i < num_clusters; i++) {
                if (total_sizes < 1000000)
                    cluster_sizes[total_sizes++] = fire_clusters[i];
            }
        }

        // Count occurrences (basic histogram)
        int count[1000] = {0};
        for (int i = 0; i < total_sizes; i++) {
            int s = cluster_sizes[i];
            if (s < 1000)
                count[s]++;
        }

        printf("Run %d: Cluster size distribution:\n", run + 1);
        for (int s = 1; s < 100; s++) {
            if (count[s] > 0)
                printf("%d\t%d\n", s, count[s]);
        }
        printf("\n");
    }

    return 0;
}

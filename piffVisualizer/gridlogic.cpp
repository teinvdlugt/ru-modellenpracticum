#include <iostream>
#include <cstdlib>
#include <fstream>
#include <cstring>
#include <list>

using namespace std;

struct pixel_color {
	GLfloat r;
	GLfloat g;
	GLfloat b;
};

struct pixel_color colorscheme[] = {
	{0,0,0},
	{88./255, 165./255, 199./255}, {106./255, 196./255, 141./255},
};
struct pixel_color border_colorscheme[] = {
	{0,0,0},
	{1, 165./255, 199./255}, 
	{1, 196./255, 141./255},
};

class grid
{
	public:

	int numof_frames;
	int * size;

	int grid_volume;
	char** grids;

	int current_frame = 0;
	
	
	void next_frame() { current_frame = (current_frame + 1) % (numof_frames - 1);}
	bool load_grid(const char* filename) {
		ifstream file(filename, ios::in|ios::binary);

		size = (int*)malloc(sizeof(int)*3);
		
		if (file.is_open()) {

			file.read((char*)(&numof_frames), sizeof(int));
			file.read((char*)(size), sizeof(int)*3);

			grid_volume = this->size[0]* this->size[1] *this->size[2];
			
			grids = (char**)malloc(sizeof(char*)*numof_frames);
			for (int f_i = 0; f_i < numof_frames; f_i++)
			{
				grids[f_i] = (char*)malloc(this->grid_volume*2);
				file.read(grids[f_i], this->grid_volume*2);
			}


			file.close();

			return true;
		} 
		else { return false; }	
	}
	int vertices_size() {
		int rv = 0;

		rv+= this->grid_volume*30;

		char* id_grid = this->grids[current_frame] + this->grid_volume;
		
		for (int x_i = 0; x_i < this->size[0]; x_i++)
			for (int y_i = 0; y_i < this->size[1] - 1; y_i++) 
				if (id_grid[x_i + y_i*this->size[1]] != id_grid[x_i + (y_i+1)*this->size[1]])
					if (id_grid[x_i + y_i*this->size[1]] == 0 || id_grid[x_i + (y_i+1)*this->size[1]] == 0)
						rv+= 30;
					else
						rv+= 60;
		for (int x_i = 0; x_i < this->size[0] - 1; x_i++)
			for (int y_i = 0; y_i < this->size[1]; y_i++) 
				if (id_grid[x_i + y_i*this->size[1]] != id_grid[x_i + 1 + y_i*this->size[1]])
					if (id_grid[x_i + y_i*this->size[1]] == 0 || id_grid[x_i + 1+ y_i*this->size[1]] == 0)
						rv+= 30;
					else
						rv+= 60;
		return rv;
	}


	bool generate_vertices(GLfloat* vertices) {
		//Lets first check how many we need: (later)
		char * current_grid = this->grids[current_frame];
		char* id_grid = current_grid + this->grid_volume;
		//Its 2d now
		//generate vertices:	
		//vertices = (GLfloat*)malloc(sizeof(GLfloat) * this->grid_volume * 2 * 3 * 5);
		for (int y_i = 0; y_i < this->size[1]; y_i++) {
			for (int x_i = 0; x_i < this->size[0]; x_i++) {
				//linksom draaien die vertices
				vertices[30*(x_i + this->size[0]*y_i) + 0] = -1 + x_i*(2.0/this->size[0]);
				vertices[30*(x_i + this->size[0]*y_i) + 1] = -1 + (y_i + 1)* (2.0/this->size[1]);
				vertices[30*(x_i + this->size[0]*y_i) + 2] = colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
				vertices[30*(x_i + this->size[0]*y_i) + 3] = colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
				vertices[30*(x_i + this->size[0]*y_i) + 4] = colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

				vertices[30*(x_i + this->size[0]*y_i) + 5] = -1 + x_i* (2.0/this->size[0]);
				vertices[30*(x_i + this->size[0]*y_i) + 6] = -1 + y_i* (2.0/this->size[1]);
				vertices[30*(x_i + this->size[0]*y_i) + 7] = colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
				vertices[30*(x_i + this->size[0]*y_i) + 8] = colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
				vertices[30*(x_i + this->size[0]*y_i) + 9] = colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

				vertices[30*(x_i + this->size[0]*y_i) + 10] = -1 + (x_i + 1)* (2.0/this->size[0]);
				vertices[30*(x_i + this->size[0]*y_i) + 11] = -1 + (y_i + 1)* (2.0/this->size[1]);
				vertices[30*(x_i + this->size[0]*y_i) + 12] = colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
				vertices[30*(x_i + this->size[0]*y_i) + 13] = colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
				vertices[30*(x_i + this->size[0]*y_i) + 14] = colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

				vertices[30*(x_i + this->size[0]*y_i) + 15] = -1 + x_i* (2.0/this->size[0]);
				vertices[30*(x_i + this->size[0]*y_i) + 16] = -1 + y_i* (2.0/this->size[1]);
				vertices[30*(x_i + this->size[0]*y_i) + 17] = colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
				vertices[30*(x_i + this->size[0]*y_i) + 18] = colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
				vertices[30*(x_i + this->size[0]*y_i) + 19] = colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

				vertices[30*(x_i + this->size[0]*y_i) + 20] = -1 + (x_i+1)* (2.0/this->size[0]);
				vertices[30*(x_i + this->size[0]*y_i) + 21] = -1 + (y_i+1)* (2.0/this->size[1]);
				vertices[30*(x_i + this->size[0]*y_i) + 22] = colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
				vertices[30*(x_i + this->size[0]*y_i) + 23] = colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
				vertices[30*(x_i + this->size[0]*y_i) + 24] = colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

				vertices[30*(x_i + this->size[0]*y_i) + 25] = -1 + (x_i+1)* (2.0/this->size[0]);
				vertices[30*(x_i + this->size[0]*y_i) + 26] = -1 + y_i* (2.0/this->size[1]);
				vertices[30*(x_i + this->size[0]*y_i) + 27] = colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
				vertices[30*(x_i + this->size[0]*y_i) + 28] = colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
				vertices[30*(x_i + this->size[0]*y_i) + 29] = colorscheme[current_grid[x_i + this->size[0]*y_i]].b;
			}
		}
		
		int counter = 30* this->grid_volume;

		GLfloat thickness = (2.0/this->size[0])/10;

		for (int x_i = 0; x_i < this->size[0]; x_i++)
			for (int y_i = 0; y_i < this->size[1] - 1; y_i++) 
				if (id_grid[x_i + y_i*this->size[1]] != id_grid[x_i + (y_i+1)*this->size[1]])
				{
					if (id_grid[x_i + y_i*this->size[1]] != 0)
					{
						vertices[counter + 0] = -1 + x_i*(2.0/this->size[0]);
						vertices[counter + 1] = -1 + (y_i+1)*(2.0/this->size[1]);
						vertices[counter + 2] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
						vertices[counter + 3] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
						vertices[counter + 4] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

						vertices[counter + 5] = -1 + x_i*(2.0/this->size[0]);
						vertices[counter + 6] = -1 + (y_i+1)*(2.0/this->size[1]) - thickness;
						vertices[counter + 7] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
						vertices[counter + 8] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
						vertices[counter + 9] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

						vertices[counter + 10] = -1 + (x_i+1)*(2.0/this->size[0]);
						vertices[counter + 11] = -1 + (y_i+1)*(2.0/this->size[1]) - thickness;
						vertices[counter + 12] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
						vertices[counter + 13] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
						vertices[counter + 14] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

						vertices[counter + 15] = -1 + x_i*(2.0/this->size[0]);
						vertices[counter + 16] = -1 + (y_i+1)*(2.0/this->size[1]);
						vertices[counter + 17] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
						vertices[counter + 18] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
						vertices[counter + 19] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

						vertices[counter + 20] = -1 + (x_i+1)*(2.0/this->size[0]);
						vertices[counter + 21] = -1 + (y_i+1)*(2.0/this->size[1]) - thickness;
						vertices[counter + 22] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
						vertices[counter + 23] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
						vertices[counter + 24] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

						vertices[counter + 25] = -1 + (x_i+1)*(2.0/this->size[0]);
						vertices[counter + 26] = -1 + (y_i+1)*(2.0/this->size[1]);
						vertices[counter + 27] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
						vertices[counter + 28] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
						vertices[counter + 29] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

						counter+=30;
					}
					if (id_grid[x_i + (y_i+1)*this->size[1]] != 0)
					{
						vertices[counter + 0] = -1 + x_i*(2.0/this->size[0]);
						vertices[counter + 1] = -1 + (y_i+1)*(2.0/this->size[1]);
						vertices[counter + 2] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].r;
						vertices[counter + 3] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].g;
						vertices[counter + 4] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].b;

						vertices[counter + 5] = -1 + x_i*(2.0/this->size[0]);
						vertices[counter + 6] = -1 + (y_i+1)*(2.0/this->size[1]) + thickness;
						vertices[counter + 7] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].r;
						vertices[counter + 8] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].g;
						vertices[counter + 9] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].b;

						vertices[counter + 10] = -1 + (x_i+1)*(2.0/this->size[0]);
						vertices[counter + 11] = -1 + (y_i+1)*(2.0/this->size[1]) + thickness;
						vertices[counter + 12] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].r;
						vertices[counter + 13] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].g;
						vertices[counter + 14] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].b;

						vertices[counter + 15] = -1 + x_i*(2.0/this->size[0]);
						vertices[counter + 16] = -1 + (y_i+1)*(2.0/this->size[1]);
						vertices[counter + 17] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].r;
						vertices[counter + 18] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].g;
						vertices[counter + 19] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].b;

						vertices[counter + 20] = -1 + (x_i+1)*(2.0/this->size[0]);
						vertices[counter + 21] = -1 + (y_i+1)*(2.0/this->size[1]) + thickness;
						vertices[counter + 22] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].r;
						vertices[counter + 23] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].g;
						vertices[counter + 24] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].b;

						vertices[counter + 25] = -1 + (x_i+1)*(2.0/this->size[0]);
						vertices[counter + 26] = -1 + (y_i+1)*(2.0/this->size[1]);
						vertices[counter + 27] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].r;
						vertices[counter + 28] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].g;
						vertices[counter + 29] = border_colorscheme[current_grid[x_i + this->size[0]*(y_i+1)]].b;

						counter+=30;
					}
				}

		for (int x_i = 0; x_i < this->size[0] - 1; x_i++)
			for (int y_i = 0; y_i < this->size[1]; y_i++) 
				if (id_grid[x_i + y_i*this->size[1]] != id_grid[x_i + 1+ y_i*this->size[1]])
				{
					if (id_grid[x_i + y_i*this->size[1]] != 0)
					{
						vertices[counter + 0] = -1 + (x_i+1)*(2.0/this->size[0]);
						vertices[counter + 1] = -1 + y_i*(2.0/this->size[1]);
						vertices[counter + 2] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
						vertices[counter + 3] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
						vertices[counter + 4] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

						vertices[counter + 5] = -1 + (x_i+1)*(2.0/this->size[0]) - thickness;
						vertices[counter + 6] = -1 + y_i*(2.0/this->size[1]);
						vertices[counter + 7] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
						vertices[counter + 8] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
						vertices[counter + 9] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

						vertices[counter + 10] = -1 + (x_i+1)*(2.0/this->size[0]) - thickness;
						vertices[counter + 11] = -1 + (y_i+1)*(2.0/this->size[1]);
						vertices[counter + 12] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
						vertices[counter + 13] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
						vertices[counter + 14] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

						vertices[counter + 15] = -1 + (x_i+1)*(2.0/this->size[0]);
						vertices[counter + 16] = -1 + y_i*(2.0/this->size[1]);
						vertices[counter + 17] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
						vertices[counter + 18] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
						vertices[counter + 19] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

						vertices[counter + 20] = -1 + (x_i+1)*(2.0/this->size[0]) - thickness;
						vertices[counter + 21] = -1 + (y_i+1)*(2.0/this->size[1]);
						vertices[counter + 22] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
						vertices[counter + 23] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
						vertices[counter + 24] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

						vertices[counter + 25] = -1 + (x_i+1)*(2.0/this->size[0]);
						vertices[counter + 26] = -1 + (y_i+1)*(2.0/this->size[1]);
						vertices[counter + 27] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].r;
						vertices[counter + 28] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].g;
						vertices[counter + 29] = border_colorscheme[current_grid[x_i + this->size[0]*y_i]].b;

						counter+=30;
					}
					if (id_grid[x_i + 1 + y_i*this->size[1]] != 0)
					{
						vertices[counter + 0] = -1 + (x_i+1)*(2.0/this->size[0]);
						vertices[counter + 1] = -1 + y_i*(2.0/this->size[1]);
						vertices[counter + 2] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].r;
						vertices[counter + 3] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].g;
						vertices[counter + 4] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].b;

						vertices[counter + 5] = -1 + (x_i+1)*(2.0/this->size[0]) + thickness;
						vertices[counter + 6] = -1 + y_i*(2.0/this->size[1]);
						vertices[counter + 7] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].r;
						vertices[counter + 8] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].g;
						vertices[counter + 9] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].b;

						vertices[counter + 10] = -1 + (x_i+1)*(2.0/this->size[0]) + thickness;
						vertices[counter + 11] = -1 + (y_i+1)*(2.0/this->size[1]);
						vertices[counter + 12] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].r;
						vertices[counter + 13] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].g;
						vertices[counter + 14] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].b;

						vertices[counter + 15] = -1 + (x_i+1)*(2.0/this->size[0]);
						vertices[counter + 16] = -1 + y_i*(2.0/this->size[1]);
						vertices[counter + 17] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].r;
						vertices[counter + 18] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].g;
						vertices[counter + 19] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].b;

						vertices[counter + 20] = -1 + (x_i+1)*(2.0/this->size[0]) + thickness;
						vertices[counter + 21] = -1 + (y_i+1)*(2.0/this->size[1]);
						vertices[counter + 22] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].r;
						vertices[counter + 23] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].g;
						vertices[counter + 24] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].b;

						vertices[counter + 25] = -1 + (x_i+1)*(2.0/this->size[0]);
						vertices[counter + 26] = -1 + (y_i+1)*(2.0/this->size[1]);
						vertices[counter + 27] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].r;
						vertices[counter + 28] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].g;
						vertices[counter + 29] = border_colorscheme[current_grid[x_i + 1 + this->size[0]*y_i]].b;

						counter+=30;
					}
				}
	}

};




bool init_grid() {

	return true;
}

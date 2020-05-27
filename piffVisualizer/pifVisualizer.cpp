/* Using standard C++ output libraries */
#include <cstdlib>
#include <iostream>
#include <thread>
using namespace std;

/* Use glew.h instead of gl.h to get all the GL prototypes declared */
#include <GL/glew.h>
/* Using SDL2 for the base window and OpenGL context init */
#include <SDL2/SDL.h>

#include "gridlogic.cpp"

GLuint program;
GLuint vbo_triangle, vbo_triangle_colors;
GLint attribute_coord2d, attribute_v_color;


/* ADD GLOBAL VARIABLES HERE LATER */
bool init_resources() {
	GLint compile_ok = GL_FALSE, link_ok = GL_FALSE;

	GLuint vs = glCreateShader(GL_VERTEX_SHADER);
	const char *vs_source =
		//"#version 100\n"  // OpenGL ES 2.0
		"#version 120\n"  // OpenGL 2.1
		"attribute vec2 coord2d;                  "
		"attribute vec3 v_color;		  "
		"varying vec3 f_color;			  "
		"void main(void) {                        "
		"  gl_Position = vec4(coord2d, 0.0, 1.0); "
		"  f_color = v_color; "
		"}";
	glShaderSource(vs, 1, &vs_source, NULL);
	glCompileShader(vs);
	glGetShaderiv(vs, GL_COMPILE_STATUS, &compile_ok);
	if (!compile_ok) {
		cerr << "Error in vertex shader" << endl;
		return false;
	}

	GLuint fs = glCreateShader(GL_FRAGMENT_SHADER);
	const char *fs_source =
		//"#version 100\n"  // OpenGL ES 2.0
		"#version 120\n"  // OpenGL 2.1
		"varying vec3 f_color;    "
		"void main(void) {        "
		"  gl_FragColor = vec4(f_color.r, f_color.g, f_color.b, 1.0); "
		"}";
	glShaderSource(fs, 1, &fs_source, NULL);
	glCompileShader(fs);
	glGetShaderiv(fs, GL_COMPILE_STATUS, &compile_ok);
	if (!compile_ok) {
		cerr << "Error in fragment shader" << endl;
		return false;
	}

	program = glCreateProgram();
	glAttachShader(program, vs);
	glAttachShader(program, fs);
	glLinkProgram(program);
	glGetProgramiv(program, GL_LINK_STATUS, &link_ok);
	if (!link_ok) {
		cerr << "Error in glLinkProgram" << endl;
		return false;
	}

	const char* attribute_name = "coord2d";
	attribute_coord2d = glGetAttribLocation(program, attribute_name);
	if (attribute_coord2d == -1) {
		cerr << "Could not bind attribute " << attribute_name << endl;
		return false;
	}
	
	attribute_name = "v_color";
	attribute_v_color = glGetAttribLocation(program, attribute_name);
	if (attribute_v_color == -1) {
		cerr << "Could not bind attribute " << attribute_name << endl;
		return false;
	}

	return true;
}

void renderPIF(SDL_Window* window, grid* g) {
	/* Clear the background as white */
	glClearColor(0, 0, 0, 0);
	glClear(GL_COLOR_BUFFER_BIT);
	
	//pardon

	glUseProgram(program);

	GLfloat* vertices;
	int vertices_size =	g->vertices_size();

	vertices = (GLfloat*)malloc(sizeof(GLfloat) *vertices_size);

	g->generate_vertices(vertices);

	g->next_frame();

	glGenBuffers(1, &vbo_triangle);
  	glBindBuffer(GL_ARRAY_BUFFER, vbo_triangle);
  	glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat)*vertices_size, vertices, GL_STATIC_DRAW);

  	glEnableVertexAttribArray(attribute_coord2d);
  	glEnableVertexAttribArray(attribute_v_color);
  	glBindBuffer(GL_ARRAY_BUFFER, vbo_triangle);
  	glVertexAttribPointer(
    		attribute_coord2d,   // attribute
    		2,                   // number of elements per vertex, here (x,y)
    		GL_FLOAT,            // the type of each element
    		GL_FALSE,            // take our values as-is
    		5 * sizeof(GLfloat), // next coord2d appears every 5 floats
    		0                    // offset of the first element
  	);
  	glVertexAttribPointer(
    		attribute_v_color,      // attribute
    		3,                      // number of elements per vertex, here (r,g,b)
    		GL_FLOAT,               // the type of each element
    		GL_FALSE,               // take our values as-is
    		5 * sizeof(GLfloat),    // next color appears every 5 floats
    		(GLvoid*) (2 * sizeof(GLfloat))  // offset of first element
  	);

	
	/* Push each element in buffer_vertices to the vertex shader */
	glDrawArrays(GL_TRIANGLES, 0, vertices_size/5);
	
	glDisableVertexAttribArray(attribute_coord2d);
	glDisableVertexAttribArray(attribute_v_color);

	/* Display the result */
	SDL_GL_SwapWindow(window);
}

void free_resources() {
	glDeleteProgram(program);
}

void mainLoop(SDL_Window* window) {
	grid g;

	g.load_grid("outputpiff");

	while (true) {
		std::this_thread::sleep_for(500ms);
		SDL_Event ev;
		while (SDL_PollEvent(&ev)) {
			if (ev.type == SDL_QUIT)
				return;
		}

		renderPIF(window, &g);
	}
}

int main(int argc, char* argv[]) {
	/* SDL-related initialising functions */
	SDL_Init(SDL_INIT_VIDEO);
	SDL_Window* window = SDL_CreateWindow("pifVisualizer",
		SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
		1000, 1000,
		SDL_WINDOW_RESIZABLE | SDL_WINDOW_OPENGL);
	SDL_GL_CreateContext(window);

	/* Extension wrangler initialising */
	GLenum glew_status = glewInit();
	if (glew_status != GLEW_OK) {
		cerr << "Error: glewInit: " << glewGetErrorString(glew_status) << endl;
		return EXIT_FAILURE;
	}

	/* When all init functions run without errors,
	   the program can initialise the resources */
	if (!init_resources())
		return EXIT_FAILURE;

	if (!init_grid())
		return EXIT_FAILURE;


	/* We can display something if everything goes OK */
	mainLoop(window);

	/* If the program exits in the usual way,
	   free resources and exit with a success */
	free_resources();
	return EXIT_SUCCESS;
}

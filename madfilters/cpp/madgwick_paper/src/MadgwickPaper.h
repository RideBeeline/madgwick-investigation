#ifndef MadgwickPaper_h
#define MadgwickPaper_h

namespace paper{

extern float deltat;
extern float beta;
extern float zeta;
extern float SEq_1, SEq_2, SEq_3, SEq_4;

}

void filterUpdate(float w_x, float w_y, float w_z, float a_x, float a_y,
                  float a_z, float m_x, float m_y, float m_z);
#endif
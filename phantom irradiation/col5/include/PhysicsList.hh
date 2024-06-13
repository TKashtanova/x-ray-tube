// PhysicsList.hh
#ifndef PhysicsList_hh
#define PhysicsList_hh

#include "G4VModularPhysicsList.hh"
#include "G4EmLivermorePhysics.hh"
#include "G4SystemOfUnits.hh"
#include "G4EmParameters.hh"


class MyPhysicsList: public G4VModularPhysicsList
{
  public:
    MyPhysicsList();
    ~MyPhysicsList();
};

#endif


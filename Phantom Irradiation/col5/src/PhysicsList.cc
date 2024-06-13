// PhysicsList.cc
#include "PhysicsList.hh"


MyPhysicsList::MyPhysicsList() 
{
  SetDefaultCutValue(10*nanometer);
  SetVerboseLevel(1);

  RegisterPhysics(new G4EmLivermorePhysics());
}

MyPhysicsList::~MyPhysicsList()
{}

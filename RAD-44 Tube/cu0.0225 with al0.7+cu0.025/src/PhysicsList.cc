// PhysicsList.cc
#include "PhysicsList.hh"


MyPhysicsList::MyPhysicsList() 
{
  SetDefaultCutValue(10*nanometer);
  SetVerboseLevel(1);

  RegisterPhysics(new G4EmLivermorePhysics());
  //RegisterPhysics(new G4EmPenelopePhysics());
}

MyPhysicsList::~MyPhysicsList()
{}

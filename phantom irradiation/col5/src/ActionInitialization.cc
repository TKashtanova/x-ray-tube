// ActionInitialization.cc
#include "ActionInitialization.hh"


MyActionInitialization::MyActionInitialization()
{} 

MyActionInitialization::~MyActionInitialization()
{}

void MyActionInitialization::BuildForMaster() const
{ 
}

void MyActionInitialization::Build() const
{ 
  MyPrimaryGeneratorAction *PrimaryGeneratorAction = new MyPrimaryGeneratorAction();
  SetUserAction(PrimaryGeneratorAction);
}
 

// ActionInitialization.cc
#include "ActionInitialization.hh"


MyActionInitialization::MyActionInitialization()
{} 

MyActionInitialization::~MyActionInitialization()
{}

void MyActionInitialization::BuildForMaster() const
{
  MyRunAction *runAction = new MyRunAction();
  SetUserAction(runAction);   
}

void MyActionInitialization::Build() const
{ 
  MyPrimaryGeneratorAction *PrimaryGeneratorAction = new MyPrimaryGeneratorAction();
  SetUserAction(PrimaryGeneratorAction);

  MyRunAction *runAction = new MyRunAction();
  SetUserAction(runAction);  
}
 

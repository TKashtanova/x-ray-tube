// ActionInitialization.hh
#ifndef ActionInitialization_hh
#define ActionInitialization_hh

#include "G4VUserActionInitialization.hh"
#include "PrimaryGeneratorAction.hh"


class MyActionInitialization : public G4VUserActionInitialization
{
  public:
    MyActionInitialization();    
    ~MyActionInitialization();

    virtual void Build() const; 
    virtual void BuildForMaster() const;
};

#endif



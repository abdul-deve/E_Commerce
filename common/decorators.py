def abstract_model(cls):
    if not hasattr(cls,"Meta"):
        class Meta:
            abstract = True
        cls.Meta = Meta
    else:
        setattr(cls.Meta,'abstract',True)
    return cls